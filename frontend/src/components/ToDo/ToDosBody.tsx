import { useEffect, useState } from "react";
import BasicToDoBody from "./BasicToDoBody";
import FullToDoContent from "./FullToDoContent";
export function ToDosBody() {

    const GET_TODOS_URL = "http://127.0.0.1:8000/todos/aleks321@gmail.com"
    const openedBodyToDoStructure = "flex flex-row h-full w-full bg-gray-900"
    const basicBodyToDoStructure = "flex flex-col h-full w-full bg-gray-900"
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