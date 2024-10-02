<script setup lang="ts">
    import { useToast } from "@/components/ui/toast";

    useHead({
        title: "Home Page",
    });

    const { toast } = useToast();
    const analyisStore = useAnalysisOptions();
    const refs = storeToRefs(analyisStore);

    function saveAnalysis() {
        $fetch("/api/analysis/save", {
            body: {
                department: refs.department.value,
                municipality: refs.municipality.value,
                institution: refs.institution.value,
                period: refs.period.value,
                reportType: analyisStore.reportType,
            },
            method: "POST",
            onResponseError(error) {
                toast({
                    title: "Oops! An error ocurred",
                    description: error.response.statusText,
                    variant: "destructive",
                });
            },
        }).then(() => {
            toast({
                title: "Saved succesfully",
            });
        });
    }
</script>

<template>
    <section :key="$route.fullPath">
        <HomeAnalysisOptions />
        <HomeAditionalOptions />
        <div class="w-full bg-background py-12">
            <div class="container px-4 md:px-6 flex gap-2">
                <Button @click="saveAnalysis"> Submit </Button>
                <Button variant="outline" @click="saveAnalysis">
                    Save Analysis
                </Button>
                <!-- <Sheet>
                    <SheetTrigger> Save Analysis </SheetTrigger>
                    <SheetContent>
                        <SheetHeader>
                            <SheetTitle> Lorem ipsum</SheetTitle>
                            <SheetDescription>
                                Lorem ipsum dolor sit amet consectetur,
                                adipisicing elit. Repellendus repellat omnis
                                modi consequatur, assumenda est. Libero aperiam
                                mollitia itaque deserunt quisquam, ipsa soluta
                                atque et porro beatae harum voluptas neque?
                            </SheetDescription>
                        </SheetHeader>
                    </SheetContent>
                </Sheet> -->
            </div>
        </div>
    </section>
</template>
