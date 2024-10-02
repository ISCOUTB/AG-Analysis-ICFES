import { z } from "zod";

export const UpdateSchema = z.object({
    email: z
        .string()
        .min(1, { message: "Email is required" })
        .email({ message: "Must be a valid email" }),

    username: z
        .string()
        .min(1, { message: "Username is required" })
        .max(50, { message: "Username is too large" }),
});
