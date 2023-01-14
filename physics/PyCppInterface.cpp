#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/eigen.h>
#include <pybind11/stl.h>

#define C_GRAV 6.67430E-11

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;


class StarSystemObject {
private:
    double mass;
    Eigen::Vector3d pos;
    Eigen::Vector3d vel;
    Eigen::Vector3d acc;

public:
    StarSystemObject(double arg_mass, Eigen::Vector3d arg_pos, Eigen::Vector3d arg_vel)
    {
        mass = arg_mass;
        pos = arg_pos;
        vel = arg_vel;
        acc = Eigen::Vector3d(0, 0, 0);
    }

    const double &get_mass(void) const {
        return mass;
    }

    const Eigen::Vector3d &get_pos(void) const {
        return pos;
    }

    const Eigen::Vector3d &get_vel(void) const {
        return vel;
    }

    const Eigen::Vector3d &get_acc(void) const {
        return acc;
    }

    void set_pos(const Eigen::Vector3d &new_pos) {
        pos = new_pos;
    }

    void set_vel(const Eigen::Vector3d &new_vel) {
        vel = new_vel;
    }

    void set_acc(const Eigen::Vector3d &new_acc) {
        acc = new_acc;
    }
};

class PyCppInterface {
private:
    std::vector<StarSystemObject> lst;

public:
    PyCppInterface(std::vector<StarSystemObject> &array) : lst(array) {}

    Eigen::Vector3d gravity_force(const StarSystemObject &a, const StarSystemObject &b) {
        Eigen::Vector3d force_direction = b.get_pos() - a.get_pos();
        double dist = force_direction.norm();
        double force_value = 0;

        force_direction.normalize();
        force_value = C_GRAV * (a.get_mass() * b.get_mass()) / (dist * dist);
        return force_direction * force_value;
    }

    // Returns the acceleration exerted on body A by body B
    Eigen::Vector3d gravity_acc(const StarSystemObject &a, const StarSystemObject &b) {
        return gravity_force(a, b) / a.get_mass();
    }

    // Compute acceleration vector from one body to the other
    Eigen::Vector3d compute_acc_for(const uint64_t body_idx) {
        uint64_t i = 0;
        Eigen::Vector3d acc = Eigen::Vector3d(0, 0, 0);

        for (i = 0; i < lst.size(); ++i) {
            if (i == body_idx)
                continue;
            else
                acc += gravity_acc(lst[body_idx], lst[i]);
        }
        return acc;
    }

    // Update all bodies position, velocity and accelerations
    void update_position(const double &dt) {
        uint64_t i = 0;

        for (i = 0; i < lst.size(); ++i) {
            lst[i].set_acc(compute_acc_for(i));
        }
        for (i = 0; i < lst.size(); ++i) {
            lst[i].set_vel(lst[i].get_vel() + (lst[i].get_acc()) * dt);
        }

        for (i = 0; i < lst.size(); ++i) {
            lst[i].set_pos(lst[i].get_pos() + (lst[i].get_vel()) * dt);
        }
    }

    std::vector<StarSystemObject> get_lst(void) {
        return lst;
    }
};

PYBIND11_MODULE(PyCppInterface, m) {
    m.doc() = "Compute position and acceleration using C++";

    py::class_<StarSystemObject>(m, "StarSystemObjectCpp")
    .def(py::init<double, Eigen::Vector3d &, Eigen::Vector3d &>())
    .def_property("pos", &StarSystemObject::get_pos, &StarSystemObject::set_pos, byref)
    .def_property("vel", &StarSystemObject::get_vel, &StarSystemObject::set_vel, byref)
    ;

    py::class_<PyCppInterface>(m, "PyCppInterface")
    .def(py::init<std::vector<StarSystemObject> &>())
    .def("update_position", &PyCppInterface::update_position)
    .def("get_lst", &PyCppInterface::get_lst, byref)
    ;
}