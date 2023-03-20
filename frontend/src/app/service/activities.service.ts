import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Activity } from '../dto/activity';
import { Street } from '../dto/street';

@Injectable({
  providedIn: 'root'
})
export class ActivitiesService {
  private apiServerUrl = environment.apiUri;

  constructor(private http: HttpClient) { 
  }

  public getActivities(): Observable<Activity[]> {
    return this.http.get<Activity[]>(`${this.apiServerUrl}/activities`);
  }

  public getStreets(): Observable<Street[]> {
    return this.http.get<Street[]>(`${this.apiServerUrl}/streets`);
  }
}
