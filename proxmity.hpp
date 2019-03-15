#pragma once

struct nav_obstacle_return {
    bool detected;
    double bearing;
    // double speed
}

class Proximity {
    public:
        Proximity();
        Proximity(bool in_detected, double in_depths[],double in_sweeps[],
            double ultrasnoics, double bearing);

        nav_obstacle_return calculate();

        void reset();

    private:
        
        double depths[64];     //8x8 array of depths from Terabee
        double sweepDistance[180]; //Distance from servo sweep, the angle is the index
        double ultrasonics[3]; //Array of depths from the ultrasonic sensors
    

};