//
// Smart Campus Network Topology
// ==============================
// Simulates a multi-subnet campus network with:
//   - 4 Student PCs in a student subnet
//   - 2 Teacher PCs in a teacher subnet
//   - 2 Admin PCs in an admin subnet
//   - 1 Campus Server in a server subnet
//   - Core router interconnecting all subnets
//   - Ethernet switches per subnet
//
// Subnet addressing (auto-assigned by Ipv4NetworkConfigurator):
//   Student subnet: 10.0.1.x/24
//   Teacher subnet: 10.0.2.x/24
//   Admin subnet:   10.0.3.x/24
//   Server subnet:  10.0.10.x/24
//

package myfirstnetwork.simulations;

import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.node.ethernet.Eth100M;
import inet.node.ethernet.EthernetSwitch;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.visualizer.canvas.integrated.IntegratedCanvasVisualizer;

network SmartCampusNetwork
{
    @display("bgb=1850,1250");
    submodules:
        // ============================================================
        // Network Auto-Configurator (IP assignment + static routing)
        // ============================================================
        configurator: Ipv4NetworkConfigurator {
            @display("p=100,50");
        }

        // ============================================================
        // Visualizer - shows packet flow, routing tables, etc.
        // ============================================================
        visualizer: IntegratedCanvasVisualizer {
            @display("p=100,150");
        }

        // ============================================================
        // Core Router - interconnects all 4 subnets
        // ============================================================
        coreRouter: Router {
            @display("p=1000,600");
        }

        // ============================================================
        // Student Subnet (10.0.1.0/24) - Switch + 4 PCs
        // ============================================================
        studentSwitch: EthernetSwitch {
            @display("p=600,300");
        }
        student1: StandardHost {
            @display("p=200,150");
        }
        student2: StandardHost {
            @display("p=350,150");
        }
        student3: StandardHost {
            @display("p=200,300");
        }
        student4: StandardHost {
            @display("p=350,300");
        }

        // ============================================================
        // Teacher Subnet (10.0.2.0/24) - Switch + 2 PCs
        // ============================================================
        teacherSwitch: EthernetSwitch {
            @display("p=600,600");
        }
        teacher1: StandardHost {
            @display("p=200,500");
        }
        teacher2: StandardHost {
            @display("p=200,650");
        }

        // ============================================================
        // Admin Subnet (10.0.3.0/24) - Switch + 2 PCs
        // ============================================================
        adminSwitch: EthernetSwitch {
            @display("p=600,900");
        }
        admin1: StandardHost {
            @display("p=200,800");
        }
        admin2: StandardHost {
            @display("p=200,950");
        }

        // ============================================================
        // Server Subnet (10.0.10.0/24) - Server directly connected
        // ============================================================
        campusServer: StandardHost {
            @display("p=1450,600");
        }

    connections:
        // Student subnet connections
        student1.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        student2.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        student3.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        student4.ethg++ <--> Eth100M <--> studentSwitch.ethg++;
        studentSwitch.ethg++ <--> Eth100M <--> coreRouter.ethg++;

        // Teacher subnet connections
        teacher1.ethg++ <--> Eth100M <--> teacherSwitch.ethg++;
        teacher2.ethg++ <--> Eth100M <--> teacherSwitch.ethg++;
        teacherSwitch.ethg++ <--> Eth100M <--> coreRouter.ethg++;

        // Admin subnet connections
        admin1.ethg++ <--> Eth100M <--> adminSwitch.ethg++;
        admin2.ethg++ <--> Eth100M <--> adminSwitch.ethg++;
        adminSwitch.ethg++ <--> Eth100M <--> coreRouter.ethg++;

        // Server subnet connection (direct to router)
        campusServer.ethg++ <--> Eth100M <--> coreRouter.ethg++;
}
