import { ReportType } from "@/types/types";

type StringKeys = ExtractByTypeExcluding<
    AnalysisOptionsState,
    string,
    ReportType
>;

export const useAnalysisOptions = defineStore("analysis-options-store", {
    state: (): AnalysisOptionsState => ({
        department: "",
        municipality: "",
        reportType: ReportType.SABER11,
    }),
    actions: {
        setDepartment(payload: string) {
            this.department = payload;
        },

        setMunicipality(payload: string) {
            if (!this.department) return;
            this.municipality = payload;
        },

        setReportType(payload: ReportType) {
            this.reportType = payload;
        },

        clear(key: StringKeys) {
            this[key] = "";
        },

        clearAll() {
            this.department = "";
            this.municipality = "";
            this.reportType = ReportType.SABER11;
        },
    },
});
