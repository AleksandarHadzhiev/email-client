//@ts-ignore
export default function SendMessage({ setSendMessageIsActivated }) {
    return (
        <section
            className="absolute bottom-0 right-0 bg-white text-black min-h-64 min-w-80 border-2 border-solid">
            <div
                className="bg-gray border-b-2 border-indigo-500">
                <button
                    onClick={() => { setSendMessageIsActivated(false) }}>
                    Close
                </button>

            </div>
            {/* Topbar */}
            {/* Body */}
            {/* Footer */}
            <p>Meow</p>
        </section>
    )
}