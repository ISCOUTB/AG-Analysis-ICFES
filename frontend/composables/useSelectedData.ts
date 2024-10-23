export default function <T extends object = {}>() {
    const data = useState<T>(() => ({}) as T);

    return {
        data,
    };
}
