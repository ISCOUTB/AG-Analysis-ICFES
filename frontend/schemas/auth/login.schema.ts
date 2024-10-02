import { z } from "zod";

export const LoginSchema = z.object({
    email: z
        .string()
        .min(1, { message: "Email is required" })
        .email({ message: "Must be a valid email" }),
    password: z.string().min(1, { message: "Password is required" }),
});

export const formFields: FormField<z.infer<typeof LoginSchema>>[] = [
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
];
