import { z } from "zod";

export const RegisterSchema = z
    .object({
        username: z
            .string()
            .min(1, { message: "Username is required" })
            .max(50, { message: "Username is too large" }),
        email: z
            .string()
            .min(1, { message: "Email is required" })
            .email({ message: "Must be a valid email" }),
        password: z
            .string()
            .min(1, { message: "Password is required" })
            .min(8, {
                message: "Password should have at least 8 characters",
            }),
        confirmPassword: z
            .string()
            .min(1, { message: "Type your password again" }),
    })
    .refine((data) => data.password === data.confirmPassword, {
        message: "Passwords must match",
        path: ["confirmPassword"],
    });

export const formFields: FormField<z.infer<typeof RegisterSchema>>[] = [
    {
        name: "username",
        label: "Username",
        type: "text",
        autocomplete: "username",
    },
    {
        name: "email",
        label: "Email",
        type: "email",
        autocomplete: "email",
    },
    {
        name: "password",
        label: "Password",
        type: "password",
        autocomplete: "off",
    },
    {
        name: "confirmPassword",
        label: "Confirm Password",
        type: "password",
        autocomplete: "off",
    },
];
