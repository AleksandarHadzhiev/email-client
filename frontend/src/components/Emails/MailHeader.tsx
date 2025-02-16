type Email = {
    from: string;
    subject: string;
    date: string;
    body: string;
    body_preview: string;
};
//@ts-ignore
export default function MailHeader({ email }) {
    return (
        <div className="flex border-l-4 border-blue-500">
            <div className="w-16 flex justify-center items-center align-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 9v.906a2.25 2.25 0 0 1-1.183 1.981l-6.478 3.488M2.25 9v.906a2.25 2.25 0 0 0 1.183 1.981l6.478 3.488m8.839 2.51-4.66-2.51m0 0-1.023-.55a2.25 2.25 0 0 0-2.134 0l-1.022.55m0 0-4.661 2.51m16.5 1.615a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V8.844a2.25 2.25 0 0 1 1.183-1.981l7.5-4.039a2.25 2.25 0 0 1 2.134 0l7.5 4.039a2.25 2.25 0 0 1 1.183 1.98V19.5Z" />
                </svg>
            </div>
            <div className="w-full h-full flex-row ml-2">
                <p className="mb-1 text-lg">{email.from}</p>
                <div className="mb-1 flex flex-row justify-between">
                    <p className="text-sm">{email.subject}</p>
                    <p className="mr-2 text-xs">{email.Date}</p>
                </div>
                <p className="text-xs">{email.body_preview}</p>
            </div>
        </div>
    )
}