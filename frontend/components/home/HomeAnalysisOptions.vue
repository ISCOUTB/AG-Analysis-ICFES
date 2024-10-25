<template>
    <section class="w-full bg-background py-12">
        <div
            id="select-options"
            class="container px-4 md:px-6 flex flex-col md:grid md:grid-cols-2 gap-4"
        >
            <div class="flex flex-col gap-8">
                <div class="flex flex-col gap-4">
                    <span class="text-3xl font-bold">Advanced Analysis</span>
                    <span class="text-gray-600 dark:text-slate-50/70"
                        >Personalize your analysis options to obtain more
                        meaninful insights.</span
                    >
                </div>
                <div class="flex flex-col gap-4">
                    <HomeSelectReportType />
                </div>
            </div>
            <div class="flex flex-col gap-4">
                <HomeSelectDepartment />
                <LazyHomeSelectMunicipality />
            </div>
        </div>
    </section>
</template>
