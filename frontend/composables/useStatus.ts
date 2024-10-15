import { Status } from "@/types/types";

export default function () {
    const status = useState<Status>(() => Status.IDLE);

    return {
        status,
    };
}
