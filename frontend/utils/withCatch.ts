export default function <T, E = Error>(
    promise: Promise<T>,
): Promise<[null, T] | [E]> {
    return promise
        .then((data: T): [null, T] => [null, data])
        .catch((error: E): [E] => [error]);
}
