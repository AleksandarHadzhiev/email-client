//@ts-ignore
export default function Email({ email }) {

    const encodedHtml = encodeURIComponent(email?.body);
    const dataUrl = `data:text/html;charset=utf-8,${encodedHtml}`;
    return (
        <section className="w-full h-full bg-gray-600 grid grid-rows-10">
            <header className="row-span-1 bg-gray-800 mt-1 mb-1 border-solid border-2 border-sky-600 rounded flex items-center mr-1 ml-1">
                <h1 className="ml-2"><strong>{email?.subject}</strong></h1>
            </header>
            <main className="row-span-9 bg-gray-600 border-solid border-2 border-sky-600 rounded mr-1 ml-1 grid grid-rows-9">
                <section id="sender-receiver-information" className="row-span-1 bg-gray-800 rounded">
                    <p className="mr-1 ml-1 mt-2" id="sender">From: <strong>{email?.from}</strong></p>
                    <div className="mr-1 ml-1 flex justify-between">
                        <p className="" id="receiver">To: <strong>You</strong></p>
                        <p className="" id="date">Date: <strong>{email?.date}</strong></p>
                    </div>
                </section>
                <section className="row-span-8 mt-2 bg-white" id="content" >
                    <iframe src={dataUrl} id="mail-content" width="100%" height="100%"></iframe>
                </section>
            </main>
        </section>
    )
}