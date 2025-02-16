import { useEffect, useState } from "react";
import BasicToDoBody from "./BasicToDoBody";
import FullToDoContent from "./FullToDoContent";
import RoutersHandler from "@/app/routersHandler";

export function ToDosBody() {
    const GET_TODOS_URL = "http://127.0.0.1:8000/todos/aleks321@gmail.com"
    // const handler = new RoutersHandler(GET_TODOS_URL)
    // 323232 / 292929 / 272727 / 222222
    const openedBodyToDoStructure = "flex flex-row h-full w-full bg-[#1C1C1C]"
    const basicBodyToDoStructure = "flex flex-col h-full w-full bg-[#1C1C1C]"
    const [isOpened, setIsOpened] = useState(false)
    const [triggeredEvent, setTrigeredEvent] = useState("")
    const [todo, setTodo] = useState({})
    const [todos, setTodos] = useState([{ title: "Title", desc: "Desc", due: "Due", email: "Email" }])
    const get = async () => {
        await fetch(GET_TODOS_URL, { method: "GET" }).then(async (res) => {
            const data = await res.json()
            console.log(data.todos)
            setTodos(data.todos)
        }).catch((err) => {
            console.log(err)
        })
    }

    console.log(isOpened)

    useEffect(() => {
        get()
    }, [triggeredEvent])
    return (
        <div className={isOpened ? openedBodyToDoStructure : basicBodyToDoStructure}>
            {isOpened ? (<>
                <BasicToDoBody todos={todos} setIsOpened={setIsOpened} setTodo={setTodo} setTrigeredEvent={setTrigeredEvent} />
                <FullToDoContent todo={todo} setIsOpened={setIsOpened} setTrigeredEvent={setTrigeredEvent} />
            </>) : <BasicToDoBody todos={todos} setIsOpened={setIsOpened} setTodo={setTodo} setTrigeredEvent={setTrigeredEvent} />}
        </div>
    )
}