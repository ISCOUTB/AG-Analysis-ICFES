import { driver } from "driver.js";
import "driver.js/dist/driver.css";

export default function () {
    function startDriver() {
        const driverInstance = driver({
            showProgress: true,
            animate: true,
            allowClose: true,
            overlayOpacity: 0.8,
        });

        driverInstance.setSteps([
            {
                element: "#select-options",
                popover: {
                    title: "Here is where you can select all the options",
                    description:
                        "Based on department, municipality, institution and period",
                },
            },
            {
                element: "#select-options__report-type",
                popover: {
                    title: "By ReportType",
                    description:
                        "This will change the analysis type. Highschools or Colleges.",
                },
            },
            {
                element: "#select-options__period",
                popover: {
                    title: "By Period",
                    description:
                        "This will be the period used to select the institutions, not the students",
                },
            },
        ]);

        driverInstance.drive();
    }

    return {
        startDriver,
    };
}
