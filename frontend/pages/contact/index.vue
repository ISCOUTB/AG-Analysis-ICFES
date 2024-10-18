<script setup lang="ts">
    import { Mail, Phone, MapPin, Clock, Send } from "lucide-vue-next";

    useHead({
        title: "Contact",
    });

    function handleSubmit(event: Event) {
        if (!(event.target instanceof HTMLFormElement)) return;

        function validateInput(
            element: Element | RadioNodeList | null,
        ): element is HTMLInputElement {
            if (
                !element ||
                element instanceof RadioNodeList ||
                !(element instanceof HTMLInputElement)
            )
                return false;
            return true;
        }

        function validateTextArea(
            element: Element | RadioNodeList | null,
        ): element is HTMLTextAreaElement {
            if (
                !element ||
                element instanceof RadioNodeList ||
                !(element instanceof HTMLTextAreaElement)
            )
                return false;
            return true;
        }

        function validateSelect(
            element: Element | RadioNodeList | null,
        ): element is HTMLSelectElement {
            if (
                !element ||
                element instanceof RadioNodeList ||
                !(element instanceof HTMLSelectElement)
            )
                return false;

            return true;
        }

        const { elements } = event.target;

        const nameInput = elements.namedItem("name");
        const emailInput = elements.namedItem("email");
        const selectItem = elements.namedItem("subject");
        const messageInput = elements.namedItem("message");

        if (
            !validateInput(nameInput) ||
            !validateInput(emailInput) ||
            !validateTextArea(messageInput) ||
            !validateSelect(selectItem)
        )
            return;

        console.log(
            nameInput.value,
            emailInput.value,
            messageInput.value,
            selectItem.value,
        );
    }
</script>

<template :key="$route.fullPath">
    <section class="w-full bg-background py-12">
        <div class="container px-4 md:px-6">
            <div class="bg-white shadow-sm">
                <div class="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
                    <h1 class="text-3xl font-bold text-gray-900">Contat us</h1>
                </div>
            </div>
            <main class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                    <div>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-6">
                            Send us a message
                        </h2>
                        <form class="space-y-6" @submit.prevent="handleSubmit">
                            <div>
                                <label
                                    htmlFor="name"
                                    class="block text-sm font-medium text-gray-700"
                                >
                                    Name
                                </label>
                                <Input
                                    name="name"
                                    placeholder="Your name"
                                    class="mt-1"
                                />
                            </div>
                            <div>
                                <label
                                    htmlFor="email"
                                    class="block text-sm font-medium text-gray-700"
                                >
                                    Email
                                </label>
                                <Input
                                    name="email"
                                    type="email"
                                    placeholder="email@example.com"
                                    class="mt-1"
                                />
                            </div>
                            <div>
                                <label
                                    htmlFor="subject"
                                    class="block text-sm font-medium text-gray-700"
                                >
                                    Subject
                                </label>
                                <Select name="subject">
                                    <SelectTrigger class="mt-1">
                                        <SelectValue
                                            placeholder="Select a subject"
                                        />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="other"
                                            >Other</SelectItem
                                        >
                                    </SelectContent>
                                </Select>
                            </div>
                            <div>
                                <label
                                    htmlFor="message"
                                    class="block text-sm font-medium text-gray-700"
                                >
                                    Message
                                </label>
                                <Textarea
                                    name="message"
                                    placeholder="Your message"
                                    class="mt-1 min-h-[150px] resize-none"
                                />
                            </div>
                            <Button class="w-full">
                                <Send class="mr-2 h-4 w-4" /> Send Message
                            </Button>
                        </form>
                    </div>
                    <div>
                        <h2 class="text-2xl font-semibold text-gray-900 mb-6">
                            Contact Information
                        </h2>
                        <div
                            class="bg-white shadow-md rounded-lg p-6 space-y-4"
                        >
                            <div class="flex items-center">
                                <Mail class="h-6 w-6 text-blue-500 mr-3" />
                                <span>info@business.com</span>
                            </div>
                            <div class="flex items-center">
                                <Phone class="h-6 w-6 text-blue-500 mr-3" />
                                <span>+34 123 456 789</span>
                            </div>
                            <div class="flex items-center">
                                <MapPin class="h-6 w-6 text-blue-500 mr-3" />
                                <span>Lorem ipsum dolor sit amet</span>
                            </div>
                            <div class="flex items-center">
                                <Clock class="h-6 w-6 text-blue-500 mr-3" />
                                <span>Monday to Friday: 9:00 - 18:00</span>
                            </div>
                        </div>
                        <div class="mt-6">
                            <h3
                                class="text-lg font-semibold text-gray-900 mb-3"
                            >
                                Our location
                            </h3>
                            <div
                                class="bg-gray-300 h-64 rounded-lg flex items-center justify-center"
                            >
                                <MapPin class="h-12 w-12 text-gray-600" />
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </section>
</template>
