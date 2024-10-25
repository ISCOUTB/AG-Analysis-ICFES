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
                element: "#select-options__department",
                popover: {
                    title: "By Department",
                    description: "Select based on the department",
                },
            },
            {
                element: "#select-options__municipality",
                popover: {
                    title: "By Municipality",
                    description: "Select based on the municipality",
                },
            },
            {
                element: "#select-options__submit",
                popover: {
                    title: "Submit button",
                },
                onHighlighted() {
                    const store = useAnalysisOptions();

                    store.setDepartment("21");

                    handleSubmit();
                },
            },
            {
                popover: {
                    title: "After clicking the analysis will start",
                    description:
                        "First getting the students count, and soon after, gathering all the students info",
                },
            },
            {
                popover: {
                    title: "That's it",
                    description:
                        "Sometimes the loading can take a while, take into consideration that. ^^",
                },
            },
        ]);

        driverInstance.drive();
    }

    return {
        startDriver,
    };
}
