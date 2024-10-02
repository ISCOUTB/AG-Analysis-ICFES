<template>
    <div>
        <button @click="addItem">Add Item</button>
        <button @click="removeItem">Remove Item</button>
        <button @click="shuffleItems">Shuffle Items</button>

        <ul v-auto-animate>
            <li v-for="item in items" :key="item">{{ item }}</li>
        </ul>
    </div>
</template>

<script setup>
    const items = ref(["Item 1", "Item 2", "Item 3"]);

    const addItem = () => {
        items.value.push(`Item ${items.value.length + 1}`);
    };

    const removeItem = () => {
        if (items.value.length > 0) {
            items.value.pop();
        }
    };

    const shuffleItems = () => {
        items.value = items.value.sort(() => Math.random() - 0.5);
    };
</script>

<style scoped>
    ul {
        list-style-type: none;
        padding: 0;
    }

    li {
        background-color: #f0f0f0;
        margin: 10px 0;
        padding: 10px;
        border-radius: 4px;
    }

    button {
        margin-right: 10px;
        margin-bottom: 10px;
    }
</style>
