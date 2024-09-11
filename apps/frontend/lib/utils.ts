import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

export const handleGoBack = () => window.history.back();

export const handleGoRoot = () => window.location.replace("/");

export const createAvatarFallback = (username?: string) => {
    return username
        ?.split(" ")
        .map((word) => word[0].toUpperCase())
        .join("");
};
