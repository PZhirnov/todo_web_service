import React from 'react'


const UserItem = ({user}) => {
   return (
       <tr>
           <td>
               {user.uid}
           </td>
           <td>
               {user.username}
           </td>
           <td>
               {user.firstName}
           </td>
           <td>
               {user.lastName}
           </td>
       </tr>
   )
}

const UsersList = ({users}) => {
    console.log(users)
    return (

        <div>
            <h1>Cписок пользователей:</h1>
            <table>
                <th>
                    uid
                </th>
                <th>
                    Name user
                </th>
                <th>
                    First Name
                </th>
                <th>
                    LastName
                </th>
                {users.map((user) => <UserItem user={user} />)}
            </table>
        </div>
            
    )
 }
 
 
 export default UsersList
 