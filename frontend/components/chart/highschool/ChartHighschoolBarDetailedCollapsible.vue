<script setup lang="ts">
    import type { z } from "zod";
    import type { HighschoolResponseArray } from "@/schemas/analysis/students.schema";

    interface Props {
        highschoolId: string;
        items: Record<string, z.infer<typeof HighschoolResponseArray>>;
    }

    defineProps<Props>();
</script>
