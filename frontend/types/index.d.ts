import type { InputHTMLAttributes, HTMLAttributes } from "vue";

declare module "#auth-utils" {
    interface User {
        id?: string;
        email?: string;
        name?: string;
        image?: string;
    }

    interface UserSession {
        loggedInAt: Int;
    }
}

declare global {
    interface ProviderInfo {
        provider: string;
        providerAccountId: string;
    }

    interface UserInfo {
        userId: string;
    }

    interface Provider {
        label: string;
        redirectTo: string;
    }

    interface NavbarLinkItem {
        label: string;
        to: string;
    }

    interface ColorModeOption {
        label: string;
        icon: string;
        action: () => void;
    }

    interface FormField<T extends object> {
        name: keyof T;
        label: string;
        type: InputHTMLAttributes["type"];

        // https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete for more info about this field
        autocomplete: InputHTMLAttributes["autocomplete"];
    }

    interface Participant {
        name: string;
        role: string;
        description: string;
        tags: string[];
        image: string;
    }

    interface AnalysisOptionsState {
        department: string;
        municipality: string;
        institution: string;
        reportType: ReportType;
        period: string;
        studentsCount: number;
    }

    interface SheetSavedAnalysisCollapsibleItem {
        label: string;
        getValue: () => string | undefined;
        renderIf: ComputedRef<boolean>;
        icon: string;
        classIcon: HTMLAttributes["class"];
    }

    type ExtractByType<T, U> = {
        [K in keyof T]: T[K] extends U ? K : never;
    }[keyof T];
}

export {};
