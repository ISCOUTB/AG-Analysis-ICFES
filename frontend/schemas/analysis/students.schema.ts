import { z } from "zod";

export const HighschoolResponse = z.object({
    id: z.number(),
    genre: z.string(),
    PUNT_ENGLISH: z.number(),
    PUNT_MATHEMATICS: z.number(),
    PUNT_SOCIAL_CITIZENSHIP: z.number(),
    PUNT_NATURAL_SCIENCES: z.number(),
    PUNT_CRITICAL_READING: z.number(),
    PUNT_GLOBAL: z.number(),
    period: z.number(),
    highschool: z.number(),
});

export const HighschoolResponseArray = z.array(HighschoolResponse);

export const CollegeResponse = z.object({
    id: z.number(),
    genre: z.string(),
    MOD_QUANTITATIVE_REASONING: z.number(),
    MOD_WRITTEN_COMMUNICATION: z.number(),
    MOD_CRITICAL_READING: z.number(),
    MOD_ENGLISH: z.number(),
    MOD_CITIZENSHIP_COMPETENCES: z.number(),
    period: z.number(),
    college: z.number(),
});

export const CollegeResponseArray = z.array(CollegeResponse);
