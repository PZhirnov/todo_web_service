import React from 'react'


const ProjectItem = ({project}) => {
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
       </tr>
   )
}

const ProjectList = ({projects}) => {
    console.log(projects)
    return (

        <div>
            <h1>Список проектов:</h1>
            <table>
                <th>
                    uid
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
                {projects.map((project) => <ProjectItem project={project} />)}
            </table>
        </div>
            
    )
 }
 
 
 export default ProjectList
 