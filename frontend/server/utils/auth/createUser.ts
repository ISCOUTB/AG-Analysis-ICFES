import { prisma } from "@/lib/prisma";
import { User } from "@prisma/client";

export default async function (
    { name, email }: { name: string; email?: string },
    { provider, providerAccountId }: ProviderInfo,
): Promise<User> {
    return await prisma.user.create({
        data: {
            name,
            email:
                email || `${name}-${provider}-${providerAccountId}@example.com`,
        },
    });
}
