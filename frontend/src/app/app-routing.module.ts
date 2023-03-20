import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ActivitiesComponent } from './activities/activities.component';
import { StreetsComponent } from './streets/streets.component';

const routes: Routes = [
  { path: '', component: ActivitiesComponent },
  { path: 'streets', component: StreetsComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
