import type { InputHTMLAttributes, HTMLAttributes } from "vue";
import type { SaveAnalysisSchema } from "@/schemas/analysis/saveAnalysis.schema";
import type { ReportType } from "@/types/types";
import type { z } from "zod";

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
    }

    interface SheetSavedAnalysisCollapsibleItem {
        label: string;
        value: string | undefined;
        renderIf: () => boolean;
        icon: string;
        classIcon: HTMLAttributes["class"];
    }

    type SheetSavedAnalysisData = z.infer<typeof SaveAnalysisSchema>;

    type SheetSavedAnalysisParsedAnalysisData = Partial<SheetSavedAnalysisData>;

    interface SheetSavedAnalysisParsedData {
        content: SheetSavedAnalysisParsedAnalysisData;
        id: string;
        createdAt: Date;
    }

    export type ExtractByTypeExcluding<T, U, Exclude> = {
        [K in keyof T]: T[K] extends U
            ? T[K] extends Exclude
                ? never
                : K
            : never;
    }[keyof T];

    interface PricingPlan {
        title: string;
        description: string;
        price: string;
        features: string[];
        message: string;
        disabled: boolean;
    }

    interface BarChartData {
        name: string;
        average: number;
        max: number;
        min: number;
    }

    interface TableData {
        name: string;
        std: number;
        variance: number;
        Q1: number;
        Q3: number;
        median: number;
    }

    interface HistogramChartData {
        minRange: number;
        maxRange: number;
        label: string;
        count: number;
    }

    interface UserDropdownMenuItem {
        label: string;
        icon?: string;
        action?: () => unknown;
        subItems?: UserDropdownMenuItem[];
    }
}

export {};
