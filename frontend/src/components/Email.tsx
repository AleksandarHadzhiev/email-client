import { JSXElementConstructor, Key, MouseEvent, ReactElement, ReactNode, ReactPortal, useState } from "react";

//@ts-ignore
export default function Email({ email }) {
    console.log(email)
    const attachments = email?.attachments
    const rowSpanForMain = attachments.length > 0 ? "row-span-8" : "row-span-9"
    const rowSpanForIFrame = attachments.length > 0 ? "row-span-7" : "row-span-9"
    const gridRowsForMain = attachments.length > 0 ? "grid-rows-8" : "grid-rows-9"
    const encodedHtml = encodeURIComponent(email?.body);
    const dataUrl = `data:text/html;charset=utf-8,${encodedHtml}`;

    // Function to convert Base64 string to Blob and trigger download
    function base64ToFile(attachment: { data: any; name: any; type?: any; }, e: MouseEvent<HTMLParagraphElement, MouseEvent>) {
        e.preventDefault()
        // Remove data URL scheme if present
        const data = attachment.data
        const name = attachment.name
        const type = attachment.type
        const byteNumbers = new Array(data.length);

        for (let i = 0; i < data.length; i++) {
            byteNumbers[i] = data.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: type });
        console.log(blob)
        const url = URL.createObjectURL(blob);

        // Create a link element to download the file
        const link = document.createElement('a');
        link.href = url;
        link.download = name;
        link.click();

        // Cleanup
        URL.revokeObjectURL(url);
    }

    return (
        <section className="w-full h-full grid grid-rows-10">
            <header className="row-span-1 bg-gray-800 mt-1 mb-1 border-solid border-2 border-sky-600 rounded flex items-center mr-1 ml-1">
                <h1 className="ml-2 row-span-1 w-full"><strong>{email?.subject}</strong></h1>
            </header>
            <main className={`${rowSpanForMain} bg-gray-600 border-solid border-2 border-sky-600 rounded mr-1 ml-1 grid ${gridRowsForMain}`}>
                <section id="sender-receiver-information" className="row-span-1 bg-gray-800 rounded">
                    <p className="mr-1 ml-1 mt-2" id="sender">From: <strong>{email?.from}</strong></p>
                    <div className="mr-1 ml-1 flex justify-between">
                        <p className="" id="receiver">To: <strong>You</strong></p>
                        <p className="" id="date">Date: <strong>{email?.date}</strong></p>
                    </div>
                </section>
                <section className={`${rowSpanForIFrame} mt-2 bg-white`} id="content" >
                    <iframe src={dataUrl} id="mail-content" width="100%" height="100%"></iframe>
                </section>
            </main>
            {attachments.length > 0 ? (
                <footer className="row-span-1 bg-gray-600 flex items-center grid grid-cols-10">
                    <div className="w-full h-full col-span-1 flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6 h-full ml-2 border-r-2 border-gray-200">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" />
                        </svg>
                    </div>
                    <div className="col-span-9 flex flex-col">
                        {attachments.map((attachment: { data: any; name: string | number | bigint | boolean | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<string | number | bigint | boolean | ReactPortal | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | null | undefined> | null | undefined; }, index: Key | null | undefined) => (
                            <p className="border-gray-700 hover:text-sky-400" onClick={(e) => { base64ToFile(attachment, e) }} key={index}>
                                {attachment.name}
                            </p>
                        ))}
                    </div>
                </footer>
            ) : null
            }
        </section >
    )
}