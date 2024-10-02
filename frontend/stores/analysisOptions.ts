export enum ReportType {
    SABER11 = "SABER11",
    SABERPRO = "SABERPRO",
}

interface State {
    department: string;
    municipality: string;
    institution: string;
    reportType: ReportType;
    period: string;
}

export const useAnalysisOptions = defineStore("analysis-options-store", {
    state: (): State => ({
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

        clear(key: keyof Omit<State, "reportType">) {
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
