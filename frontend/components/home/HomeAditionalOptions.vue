<template>
    <section class="w-full bg-gray-300/20 dark:bg-gray-900/80 py-12">
        <div
            class="container px-4 md:px-6 flex flex-col md:grid md:grid-cols-2 gap-12"
        >
            <div class="flex flex-col gap-4">
                <span class="text-3xl font-bold">Aditional Options</span>
                <span class="text-gray-600 dark:text-slate-50/70"
                    >Select the options that will be included in the
                    analysis</span
                >
            </div>
            <div
                class="flex flex-col sm:grid sm:grid-cols-2 gap-6 sm:gap-0 items-start"
            >
                <HomeAditionalOptionsCheckbox
                    label="This is the label"
                    description="Lorem Ipsum dolor sit amet"
                    :action="() => console.log('clicked')"
                />
                <HomeAditionalOptionsCheckbox
                    label="This is the label"
                    description="Lorem ipsum dolor sit amet"
                    :action="() => console.log('clicked')"
                />
            </div>
        </div>
    </section>
</template>
