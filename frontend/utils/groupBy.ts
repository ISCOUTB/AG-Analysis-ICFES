export default function <T, K extends keyof T>(
    array: T[],
    key: K,
): Record<string, T[]> {
    return array.reduce(
        (result, currentValue) => {
            const groupKey = String(currentValue[key]);

            if (!result[groupKey]) result[groupKey] = [];

            result[groupKey].push(currentValue);

            return result;
        },
        {} as Record<string, T[]>,
    );
}
