import { H3Event } from "h3";
import { UserSession } from "#auth-utils";

export default async function (
    event: H3Event,
    userSessionData: UserSession["user"],
): Promise<void> {
    await setUserSession(event, {
        user: userSessionData,
        loggedInAt: Date.now(),
    });
}
