import { ReportType } from "@/types/types";

type StringKeys = ExtractByTypeExcluding<
    AnalysisOptionsState,
    string,
    ReportType
>;

export const useAnalysisOptions = defineStore("analysis-options-store", {
    state: (): AnalysisOptionsState => ({
        department: "",
        institution: "",
        municipality: "",
        reportType: ReportType.SABER11,
        period: "",
    }),
    actions: {
        setDepartment(payload: string) {
            this.department = payload;
        },

        setMunicipality(payload: string) {
            if (!this.department) return;
            this.municipality = payload;
        },

        setInstitution(payload: string) {
            if (!this.department || !this.department) return;
            this.institution = payload;
        },

        setReportType(payload: ReportType) {
            this.reportType = payload;
        },

        setPeriod(payload: string) {
            this.period = payload;
        },

        clear(key: StringKeys) {
            this[key] = "";
        },

        clearAll() {
            this.department = "";
            this.municipality = "";
            this.institution = "";
            this.reportType = ReportType.SABER11;
            this.period = "";
        },
    },
});
