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
               {user.first_name}
           </td>
           <td>
               {user.last_name}
           </td>
           <td>
               {user.email}
           </td>
           <td>
               {user.add_datetime}
           </td>
           <td>
               {user.last_modified}
           </td>
       </tr>
   )
}

const UsersList = ({users}) => {
    return (
        <table>
            <th>
                uid
            </th>
            <th>
                Name user
            </th>
            <th>
                First name
            </th>
            <th>
                Last Name
            </th>
            <th>
                Email
            </th>
            <th>
                Add date
            </th>
            <th>
                Last modified
            </th>
            {users.map((user) => <UserItem user={user} />)}
        </table>
    )
 }
 
 
 export default UsersList
 