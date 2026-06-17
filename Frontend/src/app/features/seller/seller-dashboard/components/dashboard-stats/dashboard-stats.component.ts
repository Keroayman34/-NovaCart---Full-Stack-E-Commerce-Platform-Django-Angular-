import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatCard } from '../../../../../core/services/seller-dashboard.service';

@Component({
  selector: 'app-dashboard-stats',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard-stats.component.html',
  styleUrls: ['./dashboard-stats.component.scss']
})
export class DashboardStatsComponent {
  @Input() stats: StatCard[] = [];

  getStatCardClass(stat: StatCard): string {
    return `stat-card stat-${stat.color}`;
  }
}
