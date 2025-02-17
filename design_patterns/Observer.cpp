/**
 * Observer Design Pattern
 * 
 * Purpose: Defines one-to-many dependency between objects where many objects
 *          are notified automatically of any state changes in one object.
 * 
 * Components:
 * - JobPost: Data class containing job information
 * - JobSeeker: Observer class that receives updates
 * - JobDistributer: Subject class that sends notifications
 * 
 * Key Features:
 * - Dynamic observer registration/removal
 * - Automatic notification of all observers
 * - Uses ID system to track observers
 * 
 * Usage Example:
 *   JobDistributer jobBoard;
 *   JobSeeker seeker;
 *   jobBoard.addJobSeeker(&seeker);
 *   jobBoard.receiveJob(JobPost{"Developer"});
 */

#include <iostream>
#include <string>
#include <map>

// Note! 
// Compile with g++ -std=c++20 (+)!
#include <format>

using namespace std;

// Global ID counter for job seekers
int id = 0;

// Data class representing a job posting
class JobPost{
    public:
        JobPost(string title): _title(title){};
        string getTitle() const {return _title;};
    private:
        string _title;
};

// Observer class that receives job notifications
class JobSeeker{
    public:
        // Initialize with unique ID
        JobSeeker(): _id(++id){};
        
        // Receive and process job notification
        void readJobTitle(const JobPost& job){ cout << format("a new job: {}! I'm job seeker number {}", job.getTitle(), _id) << endl;};
        
        int get_id(){return _id;};
    private:
        int _id;  // Unique identifier for each seeker
};

// Subject class that distributes job notifications
class JobDistributer{
    public:
        // Register new observer
        void addJobSeeker(JobSeeker* seeker){ _listeners[seeker->get_id()] = seeker;};
        
        // Remove observer
        void detachJobSeeker(int id){
            if (!_listeners.erase(id)) {
                cout << "ERROR: No job seeker was found with that id!" << endl;
            }
        }
        
        // Notify all observers of new job
        void receiveJob(const JobPost& job){
            for (auto& it: _listeners){
                it.second->readJobTitle(job);
            }
        }
    private:
        map<int, JobSeeker*> _listeners;  // Map of registered observers
};


int main(){
    // Create job distributor and observers
    JobDistributer jobDest;
    JobSeeker jobSeekOne;
    JobSeeker jobSeekTwo;
    JobSeeker jobSeekThree;
    JobSeeker jobSeekFour;

    // Register observers
    jobDest.addJobSeeker(&jobSeekOne);
    jobDest.addJobSeeker(&jobSeekTwo);
    jobDest.addJobSeeker(&jobSeekThree);
    jobDest.addJobSeeker(&jobSeekFour);

    // Test observer removal
    jobDest.detachJobSeeker(jobSeekThree.get_id());
    jobDest.detachJobSeeker(10);  // Invalid ID

    // Notify observers of new job
    jobDest.receiveJob(JobPost{"Seasame Counter"});
    return 0;
}