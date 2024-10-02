interface State {
    steps: string[];
}

export const useUpdatePassword = defineStore("update-password", {
    state: (): State => ({
        steps: [],
    }),
    getters: {
        hasCompletedStep:
            ({ steps }) =>
            (step: string) => {
                return steps.some((current) => current === step);
            },
    },
    actions: {
        markAsCompleted(step: string) {
            this.steps.push(step);
        },

        clear() {
            this.steps.length = 0;
        },
    },
});
