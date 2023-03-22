import { Component, OnInit } from '@angular/core';
import { Activity } from '../dto/activity';
import { ActivitiesService } from '../service/activities.service';

@Component({
  selector: 'app-activities',
  templateUrl: './activities.component.html',
  styleUrls: ['./activities.component.css']
})
export class ActivitiesComponent implements OnInit {
  activities: Activity[] = [];
  page: number = 0;

  constructor(private service: ActivitiesService) { }

  ngOnInit(): void {
    this.service.getActivities().subscribe({
      next: (response: Activity[]) => this.onResponse(response)
    });
  }

  onResponse(response: Activity[]): void {
    this.activities = response;
  }

  nextPage(): void {
    this.getPage(++this.page);
  }

  prevPage(): void {
    if(this.page > 0) {
      this.getPage(--this.page);
    }
  }

  getPage(page: number): void {
    this.service.getActivities(page).subscribe({
      next: (response: Activity[]) => this.onResponse(response)
    });
  }

}
