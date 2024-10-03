import { z } from "zod";
import { ReportType } from "@/types/types";

export const SaveAnalysisSchema = z.object({
    department: z.string(),
    municipality: z.string(),
    institution: z.string(),
    period: z.string(),
    reportType: z.nativeEnum(ReportType),
});
