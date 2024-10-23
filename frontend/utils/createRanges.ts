interface Args {
    min: number;
    max: number;
    steps: number;
}

interface ReturnType {
    minRange: number;
    maxRange: number;
}

export default function ({ min, max, steps }: Args): ReturnType[] {
    if (min > max) [min, max] = [max, min];

    const stepSize = max / steps;

    return Array.from({ length: max / steps }).map((_, index) => {
        let minRange = index * stepSize;
        const maxRange = minRange + stepSize;

        if (index) minRange++;

        return {
            minRange,
            maxRange,
        };
    });
}
