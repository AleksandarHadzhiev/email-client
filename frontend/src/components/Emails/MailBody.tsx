'use client'
import Email from "./Email"
import LoadingScreen from "../loadingScreen"


//@ts-ignore
export default function MailBody({ email }) {
    console.log(email)
    return (
        <section className="col-span-7 h-full w-full">
            {email !== null ? (
                <Email email={email} />
            ) : (
                <LoadingScreen />
            )}
        </section>
    )
}
