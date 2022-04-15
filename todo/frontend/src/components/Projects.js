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
               {project.hrefRepo}
           </td>
           <td>
               {project.addDate}
           </td>
           <td>
                <Link to={`projects/${project.id}/${project.name}/`} class="btn btn-dark">Открыть задачи</Link>
           </td>
           <td>
               <button type="button" onClick={() => deleteProject(project.id)} >Удалить проект</button>
           </td>
           <td>
               <button type="button" onClick={() => console.log('edit')} >Редактировать</button>
           </td>

       </tr>
   )
}

const ProjectList = ({projects, deleteProject}) => {

    console.log(projects)
    

    function docLocation(nameAction) {
        // Обработка перехода на форму создания проекта
        let createBtn = document.getElementById("createBtn");
        console.log('events');
        console.log(createBtn)
        // document.location.href = `/projects/${nameAction}/`
        // if (createBtn) {
        //     createBtn.addEventListener("click", () => {console.log('create')})
        // }
    }


    return (

        <div>
            <h1>Список проектов:</h1>
            {/* <button type="button" id="createBtn" onClick={() => docLocation('create')}>Создать проект</button> */}
            <Link to='/projects/create/' class='btn'>Создать проект</Link>
            <table>
                <th>
                    id
                </th>
                <th>
                    Наименование проекта
                </th>
                <th>
                    Описание проекта
                </th>
                <th>
                    Ссылка на репозиторий
                </th>
                <th>
                    Дата добавления проекта
                </th>
                <th>
                    Задачи на проекте
                </th>
                <th>
                    Удалить проект
                </th>
                {projects.map((project) => <ProjectItem project={project} deleteProject={deleteProject}/>)}
            </table>
            {
                //addEvents()
            }
        </div>
            
    )
 }
 
 
 export default ProjectList
 