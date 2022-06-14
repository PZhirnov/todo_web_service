import React from 'react';
import { Link, button } from 'react-router-dom';


const ProjectItem = ({project, deleteProject}) => {
   return (
       <tr>
           <td>
               {project.id}
           </td>
           <td>
               {project.name}
           </td>
           <td>
               {project.description}
           </td>
           <td>
               <a href={project.hrefRepo} target='_blank'>{project.hrefRepo}</a>
           </td>
           <td>
               {project.addDate}
           </td>
           <td>
               <ul>
                {project.userOnProject.map((user) => <li class="userSmall">{user.username}</li>)} 
               </ul>
           </td>
           <td>
                <Link to={`projects/tasks/${project.id}/${project.name}/`} class="btn btn-dark">Список</Link>
                <Link to={`projects/${project.id}/tasks/create/`} class="btn btn-dark">Новая</Link>
           </td>
           <td>
               <button type="button" onClick={() => deleteProject(project.id)} class="btn_action">Удалить</button>
               <Link to={`projects/${project.id}/`} class="btn btn-dark" >Редактировать</Link>
           </td>

       </tr>
   )
}

const ProjectList = ({projects, deleteProject, searchProject}) => {

    console.log(projects)
    

    function docLocation(nameAction) {
        // Обработка перехода на форму создания проекта
        let createBtn = document.getElementById("createBtn");
        console.log('events');
        console.log(createBtn)

    }

    function docLocation(nameAction) {
        // Обработка перехода на форму создания проекта
        let createBtn = document.getElementById("createBtn");
        console.log('events');
        console.log(createBtn)

    }

    function search() {
        // Обработка перехода на форму создания проекта
        let fieldSearch = document.querySelector(".fieldSearch");
        console.log(fieldSearch.value);
        let res = searchProject(fieldSearch.value)


    }


    return (

        <div>
            <h1>Список проектов:</h1>
            {/* <button type="button" id="createBtn" onClick={() => docLocation('create')}>Создать проект</button> */}
            <div class = "search">
                <label for="fieldSearch">Введите наименование проекта: </label>
                <input type="text" class="fieldSearch"></input>
                <button type="button" onClick={(event) => search()} class='btn_action'>Найти</button>
            </div>
                
            
            <table>
                
                <th>
                    id
                </th>
                <th>
                    Наименование 
                </th>
                <th>
                    Описание
                </th>
                <th>
                    Ссылка
                </th>
                <th>
                    Дата добавления
                </th>
                <th>
                    Пользователи
                </th>
                <th>
                    Задачи
                </th>
                <th>
                    Действия
                </th>
                {projects.map((project) => <ProjectItem project={project} deleteProject={deleteProject}/>)}
                <tr className="createRow">
                    <div class="createBtn">
                        <Link to='/projects/create/' class='createBtn'> + Создать проект</Link>
                    </div>    
                </tr>
            </table>
        </div>
            
    )
 }
 
 
 export default ProjectList
 