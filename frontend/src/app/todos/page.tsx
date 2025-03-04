'use client'

import Navbar from "@/components/navigation"
import { ToDosBody } from "@/components/ToDo/ToDosBody"
export default function Index() {
    return (
        <div className="h-screen flex flex-col">
            <Navbar />
            <main className="grow">
                <ToDosBody />
            </main>
        </div>
    )
}