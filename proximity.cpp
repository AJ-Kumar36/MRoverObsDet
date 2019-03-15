#include "pid.hpp"
#include <algorithm>
// bool detected;
//        double depths[64];     //8x8 array of depths from Terabee
//        double sweepDistance[180]; //Distance from servo sweep, the angle is the index
//        double ultrasonics[3]; //Array of depths from the ultrasonic sensors
//        double bearing;


proximity::proximity(){
    detected = false;
    fill_n(depths, 64, -1);
    fill_n(sweepDistance, 180, -1)
    fill_n(ultrasonics, 3, -1);
    bearing = 90; // straight

}

proximity::proximity(bool in_detected, double in_depths[],double in_sweeps[],
            double in_ultrasonics[], double in_bearing) : detected(in_detected), 
            depths(in_depths), sweepDistance(in_sweeps), ultrasonics(in_ultrasonics[]),
            bearing(in_bearing) { }

double proximity::calculate(){


}
