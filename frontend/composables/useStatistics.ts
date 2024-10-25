import { mean } from "lodash";
import { std } from "mathjs";

export default function () {
    function skewness(data: number[]): number {
        if (data.length < 3) return NaN;

        const average = mean(data);
        const standardDeviation = Number(std(data));
        const { length } = data;

        if (standardDeviation === 0) return 0;

        const sumCubedDeviations = data.reduce((sum, value) => {
            const deviation = value - average;
            return sum + Math.pow(deviation, 3);
        }, 0);

        return sumCubedDeviations / (length * Math.pow(standardDeviation, 3));
    }

    function kurtosis(data: number[]): number {
        if (data.length < 4) return NaN;

        const average = mean(data);
        const standardDeviation = Number(std(data));
        const { length } = data;

        if (standardDeviation === 0) return 0;

        const sumQuarticDeviations = data.reduce((sum, value) => {
            const deviation = value - average;
            return sum + Math.pow(deviation, 4);
        }, 0);

        return (
            sumQuarticDeviations / (length * Math.pow(standardDeviation, 4)) - 3
        );
    }

    return {
        skewness,
        kurtosis,
    };
}
