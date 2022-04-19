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
               {project.userOnProject.map((user) => user.username).join(', \n')}
           </td>
           <td>
                <Link to={`projects/tasks/${project.id}/${project.name}/`} class="btn btn-dark">Список задач</Link>
                <Link to={`projects/${project.id}/tasks/create/`} class="btn btn-dark">Новая</Link>
           </td>
           <td>
               <button type="button" onClick={() => deleteProject(project.id)} >Удалить проект</button>
           </td>
           <td>
               {/* <button type="button" onClick={() => console.log('edit')} >Редактировать</button> */}
               <Link to={`projects/${project.id}/`} class="btn btn-dark">Редактировать проект</Link>
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
                    Name
                </th>
                <th>
                    Description
                </th>
                <th>
                    Link
                </th>
                <th>
                    Add date
                </th>
                <th>
                    Users count
                </th>
                <th>
                    Tasks
                </th>
                <th>
                    Delete
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
 