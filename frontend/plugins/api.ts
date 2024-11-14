import type { $Fetch } from "ofetch";
import { useToast } from "@/components/ui/toast";
import type { NitroFetchRequest } from "nitropack";

declare module "#app" {
    interface NuxtApp {
        $api: $Fetch;
    }
}

export default defineNuxtPlugin({
    setup() {
        const { API_URL } = useRuntimeConfig().public;

        const api = $fetch.create<unknown, NitroFetchRequest>({
            baseURL: `${API_URL}/api/saber`,
            onResponseError({ response }) {
                const { toast } = useToast();

                toast({
                    title: "Oops! An error ocurred",
                    description: response.statusText,
                    variant: "destructive",
                });
            },
        });

        return {
            provide: {
                api,
            },
        };
    },
});
