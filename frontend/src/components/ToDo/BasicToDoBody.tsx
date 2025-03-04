import { ReactElement, JSXElementConstructor, ReactNode, ReactPortal, Key } from "react"
import ToDoComponent from "./ToDoComponent"


//@ts-ignore
export default function BasicToDoBody({ todos, setIsOpened, setTodo, setTrigeredEvent }) {
    const updateStructure = (todo: { title: string | number | bigint | boolean | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | Promise<string | number | bigint | boolean | ReactPortal | ReactElement<unknown, string | JSXElementConstructor<any>> | Iterable<ReactNode> | null | undefined> | null | undefined }) => {
        setIsOpened(true)
        setTodo(todo)
    }

    const DELETE_TODO_URL = "http://127.0.0.1:8000/todo/"

    async function deleteToDo(id: Number) {
        await fetch(DELETE_TODO_URL + id.toString(), { method: "DELETE" }).then(async (res) => {
            const data = await res.json()
            setTrigeredEvent("delete")
        }).catch((err) => {
            alert(err)
        })
    }

    return (
        <div className="flex flex-col w-full h-full">
            <div className="grow">
                <ul className="space-y-2 mt-2 font-medium">
                    {todos.map((todo: { title: any; id?: any }, index: Key | null | undefined) => (
                        <li
                            className="h-12 hover:bg-gray-800 bg-[#272727] rounded-sm ml-2 mr-2 flex items-center align-center "
                            key={index}
                        >
                            <div className="w-[95%] flex space-x-2" onClick={() => { updateStructure(todo) }}>
                                <div className="ml-2 border-2 border-white hover:border-gray-400 w-6 h-6 rounded-full "></div>
                                <p><strong>{todo.title}</strong></p>
                            </div>
                            <p className="hover:text-blue-400" onClick={() => {
                                deleteToDo(todo.id)
                            }}>
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="size-6">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                                </svg>
                            </p>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="mb-2 ml-2 mr-2 rounded-full" ><ToDoComponent setTrigeredEvent={setTrigeredEvent} /></div>
        </div>
    )
}