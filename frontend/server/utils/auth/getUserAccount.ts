import { prisma } from "@/lib/prisma";
import { Account } from "@prisma/client";

export default async function ({
    provider,
    providerAccountId,
}: ProviderInfo): Promise<Account | null> {
    return await prisma.account.findUnique({
        where: {
            provider_providerAccountId: {
                provider,
                providerAccountId,
            },
        },
    });
}
