import React from "react";


// Функция получает индексы выбранных проектов из массива select
function getSelectedIndexes (oListbox)
{
  var arrIndexes = new Array;
  for (var i=0; i < oListbox.options.length; i++)
  {
      if (oListbox.options[i].selected) arrIndexes.push(i);
  }
  return arrIndexes;
};

// Функция получает id выбранных проектов из select
function getSelectedId (oListbox)
{
  var arrId = new Array;
  for (var i=0; i < oListbox.options.length; i++)
  {
      if (oListbox.options[i].selected) arrId.push(
          {id: oListbox.options[i].value, username: oListbox.options[i].innerHTML}
          );
  }
  return arrId;
};


class ProjectForm extends React.Component {

    constructor (props) {
        super(props)
        console.log(props);
        if (props.edit) {
            let id_project = document.location.pathname.replaceAll('projects/', '').replaceAll('/', '').trim();
            let project = props.projects.filter((item) => item.id == id_project)[0]
            console.log(project)
            this.state = project
            // Выделим пользователей в select
            let usersOnProjectId = project['userOnProject']
            //console.log(usersList)
            //SelectUsersOnProject(usersList, usersOnProjectId)

        } else {
            this.state = {name: '', description: '', hrefRepo: '', addDate: '', lastModified: '', userOnProject: []}    
        }  
    }

    handleChange(event) {
        // Получим массив id выбранных пользователей, чтобы потом добавить их на проект
        let selectedUsers = document.getElementById('usersOnProject')
        let idUsers = getSelectedId(selectedUsers)
        this.setState(
            {
                [event.target.name]: event.target.value,
                userOnProject: idUsers,
            }
        );
        console.log(this.state);
        console.log(this.state.userOnProject);
    }

    handleSubmit(event) {
        if (!this.props.edit) {
            this.props.createProject(this.state)
            this.props.edit = true
        } else {
            console.log(this.state.id)
            this.props.editProject(this.state.id, this.state)
        }
        event.preventDefault()
    }

    render() {
        return(
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <div className="main">
                    <div className="field">
                        <label for='name'>Наименование проекта:</label>
                        <input type='text' className="form-control" name="name" value={this.state.name} onChange={(event) => this.handleChange(event)}/>
                    </div>
                    <div className="field">
                        <label for='description'>Описание проекта:</label>
                        <textarea rows="4" cols="120" className="form-control" name='description' value={this.state.description} onChange={(event) => this.handleChange(event)}>

                        </textarea>
                    </div>
                    <div className="field">
                        <label for='hrefRepo'>Ссылка на репозиторий:</label>
                        <input type='url' className="form-control" name="hrefRepo" value={this.state.hrefRepo} onChange={(event) => this.handleChange(event)}/>
                    </div>
                    <div className="field">
                        <label for='usersOnProject'>Пользователи на проекте:</label>
                        <ul>
                        {this.state.userOnProject.map((user) => <li class='userLi'>{user.username}</li>)}

                        {/* {this.is_authenticated() ? <button onClick={ () => this.logout()}>Выход</button> : <Link to='/login'>Вход</Link>}    */}

                        
                        
                        </ul>
                        
                        <select size='10' className="form-control" multiple="multiple" id='usersOnProject' onChange={(event) => this.handleChange(event)} >
                            {this.props.users.map(
                                (user) => 
                                <option value={user.id} onClick={(event) => this.handleChange(event)}>{user.username}</option>)}
                        
                        </select>
                    </div>
                    
                    <button type="submit" className="btn_action_large">Сохранить</button>
                </div>
            </form>   
        )
    }
}
// {this.state.userOnProject.map((user) => user.id).includes(15)}
export default ProjectForm